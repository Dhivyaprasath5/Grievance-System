"""
OCR Service for extracting text from images
Supports: PNG, JPG, JPEG formats
"""
import os
import pytesseract
from PIL import Image
import io


class OCRService:
    """Service for extracting text from images using Tesseract OCR"""
    
    SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg']
    
    @staticmethod
    def preprocess_image(image):
        """
        Preprocess image for better OCR accuracy
        - Convert to grayscale
        - Enhance contrast
        """
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        return image
    
    @staticmethod
    def extract_text_from_image(image_file):
        """
        Extract text from an image file
        
        Args:
            image_file: File object or bytes
            
        Returns:
            dict: {
                'success': bool,
                'text': str,
                'error': str (if failed)
            }
        """
        try:
            # Read image
            if isinstance(image_file, bytes):
                image = Image.open(io.BytesIO(image_file))
            else:
                image = Image.open(image_file)
            
            # Validate format
            image_format = image.format.lower() if image.format else ''
            if image_format not in OCRService.SUPPORTED_FORMATS:
                return {
                    'success': False,
                    'error': f'Unsupported format. Supported: {", ".join(OCRService.SUPPORTED_FORMATS)}'
                }
            
            # Preprocess image
            processed_image = OCRService.preprocess_image(image)
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(processed_image)
            
            # Clean up text
            text = text.strip()
            
            if not text:
                return {
                    'success': False,
                    'error': 'No text found in image'
                }
            
            return {
                'success': True,
                'text': text
            }
            
        except pytesseract.TesseractNotFoundError:
            return {
                'success': False,
                'error': 'Tesseract OCR is not installed. Please install it first.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'OCR processing failed: {str(e)}'
            }
    
    @staticmethod
    def is_tesseract_installed():
        """Check if Tesseract OCR is installed"""
        try:
            pytesseract.get_tesseract_version()
            return True
        except:
            return False
